'use client';

import type { SectionSchema } from '@/lib/schema';
import { TimelineSection } from './TimelineSection';
import { GridListSection } from './GridListSection';
import { TextContentSection } from './TextContentSection';
import { GallerySection } from './GallerySection';

interface SectionRendererProps {
    section: SectionSchema;
    index: number;
}

/**
 * Section Renderer - Dispatcher component that routes to the appropriate layout
 * based on the section type from the Vision API parser
 */
export function SectionRenderer({ section, index }: SectionRendererProps) {
    switch (section.type) {
        case 'timeline':
            return <TimelineSection section={section} index={index} />;

        case 'grid-list':
            return <GridListSection section={section} index={index} />;

        case 'text-content':
            return <TextContentSection section={section} index={index} />;

        case 'gallery':
            return <GallerySection section={section} index={index} />;

        default:
            // Fallback for unknown types
            console.warn(`Unknown section type: ${section.type}`);
            return null;
    }
}
