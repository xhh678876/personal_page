'use client';

import { motion } from 'framer-motion';
import type { SectionSchema } from '@/lib/schema';

interface GridListSectionProps {
    section: SectionSchema;
    index: number;
}

/**
 * Grid List Section - Bento-style card grid layout
 * Perfect for: Publications, Projects, Patents, Talks
 */
export function GridListSection({ section, index }: GridListSectionProps) {
    return (
        <motion.section
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
            className="mb-16"
        >
            {/* Section Header */}
            <h2 className="text-3xl font-bold mb-8 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                {section.title}
            </h2>

            {/* Responsive Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {section.items.map((item, itemIndex) => (
                    <motion.div
                        key={item.id || itemIndex}
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.5, delay: itemIndex * 0.05 }}
                        whileHover={{ y: -8, transition: { duration: 0.2 } }}
                        className="group"
                    >
                        {/* Glassmorphism Card */}
                        <div className="h-full bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-200 dark:border-gray-700 hover:border-purple-400 dark:hover:border-purple-600">
                            {/* Image Thumbnail (if exists) */}
                            {item.image && (
                                <div className="mb-4 rounded-lg overflow-hidden">
                                    <img
                                        src={item.image}
                                        alt={item.title}
                                        className="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-300"
                                    />
                                </div>
                            )}

                            {/* Title */}
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                                {item.title}
                            </h3>

                            {/* Subtitle */}
                            {item.subtitle && (
                                <p className="text-sm text-gray-600 dark:text-gray-400 font-medium mb-2 italic">
                                    {item.subtitle}
                                </p>
                            )}

                            {/* Date */}
                            {item.date && (
                                <p className="text-xs text-gray-500 dark:text-gray-500 mb-3">
                                    {item.date}
                                </p>
                            )}

                            {/* Description */}
                            {item.description && (
                                <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed mb-3 line-clamp-3">
                                    {item.description}
                                </p>
                            )}

                            {/* Tags */}
                            {item.tags && item.tags.length > 0 && (
                                <div className="flex flex-wrap gap-1.5 mt-3">
                                    {item.tags.slice(0, 5).map((tag, tagIndex) => (
                                        <span
                                            key={tagIndex}
                                            className="px-2 py-0.5 text-xs font-medium text-pink-700 dark:text-pink-300 bg-pink-100 dark:bg-pink-900/30 rounded-full"
                                        >
                                            {tag}
                                        </span>
                                    ))}
                                    {item.tags.length > 5 && (
                                        <span className="px-2 py-0.5 text-xs font-medium text-gray-600 dark:text-gray-400">
                                            +{item.tags.length - 5}
                                        </span>
                                    )}
                                </div>
                            )}

                            {/* Metadata (e.g., citations) */}
                            {item.metadata && Object.keys(item.metadata).length > 0 && (
                                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-600 dark:text-gray-400">
                                    {item.metadata.citations && (
                                        <span className="mr-3">📊 {item.metadata.citations} citations</span>
                                    )}
                                    {item.metadata.type && (
                                        <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded">
                                            {item.metadata.type}
                                        </span>
                                    )}
                                </div>
                            )}

                            {/* Link */}
                            {item.link && (
                                <a
                                    href={item.link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center mt-4 text-purple-600 dark:text-purple-400 hover:underline text-sm font-semibold"
                                >
                                    View →
                                </a>
                            )}
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.section>
    );
}
