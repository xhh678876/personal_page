import { useState, useCallback } from 'react';
import * as pdfjsLib from 'pdfjs-dist';
import type { PDFDocumentProxy } from 'pdfjs-dist';

// Configure pdfjs worker for Next.js 14 App Router
if (typeof window !== 'undefined') {
    pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;
}

interface UsePdfToImageReturn {
    images: string[];
    loading: boolean;
    error: string | null;
    convertPdfToImages: (file: File) => Promise<string[]>;
    reset: () => void;
}

const MAX_PAGES_WARNING = 10;
const RENDER_SCALE = 2.0; // Higher DPI for better Vision API recognition

/**
 * Custom React Hook for converting PDF files to Base64 image arrays
 * Suitable for sending to Vision-Language Models (e.g., gpt-4o)
 * 
 * @returns {UsePdfToImageReturn} State and methods for PDF-to-image conversion
 */
export function usePdfToImage(): UsePdfToImageReturn {
    const [images, setImages] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const reset = useCallback(() => {
        setImages([]);
        setLoading(false);
        setError(null);
    }, []);

    const convertPdfToImages = useCallback(async (file: File): Promise<string[]> => {
        setLoading(true);
        setError(null);
        setImages([]);

        try {
            // Validate file type
            if (file.type !== 'application/pdf') {
                throw new Error('Invalid file type. Please upload a PDF file.');
            }

            // Read file as ArrayBuffer
            const arrayBuffer = await file.arrayBuffer();

            // Load PDF document
            const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
            const pdf: PDFDocumentProxy = await loadingTask.promise;

            const numPages = pdf.numPages;

            // Warn if PDF is too large
            if (numPages > MAX_PAGES_WARNING) {
                console.warn(
                    `PDF has ${numPages} pages. Processing may be slow and Vision API costs will be higher.`
                );
                // You can throw an error here if you want to enforce a hard limit
                // throw new Error(`PDF has too many pages (${numPages}). Maximum is ${MAX_PAGES_WARNING}.`);
            }

            const imagePromises: Promise<string>[] = [];

            // Process each page
            for (let pageNum = 1; pageNum <= numPages; pageNum++) {
                imagePromises.push(
                    (async () => {
                        try {
                            const page = await pdf.getPage(pageNum);
                            const viewport = page.getViewport({ scale: RENDER_SCALE });

                            // Create offscreen canvas
                            const canvas = document.createElement('canvas');
                            const context = canvas.getContext('2d');

                            if (!context) {
                                throw new Error('Failed to get canvas 2D context');
                            }

                            canvas.width = viewport.width;
                            canvas.height = viewport.height;

                            // Render PDF page to canvas
                            await page.render({
                                canvasContext: context,
                                viewport: viewport,
                            }).promise;

                            // Convert canvas to Base64 data URL
                            const dataUrl = canvas.toDataURL('image/png');

                            // Cleanup
                            page.cleanup();

                            return dataUrl;
                        } catch (pageError) {
                            console.error(`Error rendering page ${pageNum}:`, pageError);
                            throw new Error(`Failed to render page ${pageNum}`);
                        }
                    })()
                );
            }

            // Wait for all pages to be converted
            const convertedImages = await Promise.all(imagePromises);

            setImages(convertedImages);
            setLoading(false);

            return convertedImages;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
            console.error('PDF to Image conversion error:', err);
            setError(errorMessage);
            setLoading(false);
            throw err;
        }
    }, []);

    return {
        images,
        loading,
        error,
        convertPdfToImages,
        reset,
    };
}
