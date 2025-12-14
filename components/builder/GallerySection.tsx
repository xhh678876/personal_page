'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';
import type { SectionSchema } from '@/lib/schema';

interface GallerySectionProps {
    section: SectionSchema;
    index: number;
}

/**
 * Gallery Section - Image gallery with lightbox
 * Perfect for: Posters, Lab Photos, Visualizations
 */
export function GallerySection({ section, index }: GallerySectionProps) {
    const [selectedImage, setSelectedImage] = useState<string | null>(null);

    return (
        <>
            <motion.section
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-100px' }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="mb-16"
            >
                {/* Section Header */}
                <h2 className="text-3xl font-bold mb-8 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                    {section.title}
                </h2>

                {/* Masonry Grid */}
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {section.items.map((item, itemIndex) => (
                        <motion.div
                            key={item.id || itemIndex}
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.4, delay: itemIndex * 0.05 }}
                            whileHover={{ scale: 1.05 }}
                            className="group relative cursor-pointer overflow-hidden rounded-lg shadow-lg"
                            onClick={() => item.image && setSelectedImage(item.image)}
                        >
                            {/* Image */}
                            {item.image && (
                                <img
                                    src={item.image}
                                    alt={item.title}
                                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                                />
                            )}

                            {/* Overlay on Hover */}
                            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                                <h3 className="text-white font-bold text-sm mb-1">
                                    {item.title}
                                </h3>
                                {item.subtitle && (
                                    <p className="text-gray-300 text-xs">{item.subtitle}</p>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </motion.section>

            {/* Lightbox Modal */}
            {selectedImage && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4"
                    onClick={() => setSelectedImage(null)}
                >
                    <motion.img
                        initial={{ scale: 0.8 }}
                        animate={{ scale: 1 }}
                        exit={{ scale: 0.8 }}
                        src={selectedImage}
                        alt="Expanded view"
                        className="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
                        onClick={(e) => e.stopPropagation()}
                    />
                    <button
                        onClick={() => setSelectedImage(null)}
                        className="absolute top-4 right-4 text-white text-4xl hover:text-gray-300 transition-colors"
                        aria-label="Close"
                    >
                        ×
                    </button>
                </motion.div>
            )}
        </>
    );
}
