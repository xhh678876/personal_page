'use client';

import { motion } from 'framer-motion';
import type { SectionSchema } from '@/lib/schema';

interface TimelineSectionProps {
    section: SectionSchema;
    index: number;
}

/**
 * Timeline Section - Vertical chronological layout
 * Perfect for: Education, Work History, Awards
 */
export function TimelineSection({ section, index }: TimelineSectionProps) {
    return (
        <motion.section
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
            className="mb-16"
        >
            {/* Section Header */}
            <h2 className="text-3xl font-bold mb-8 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                {section.title}
            </h2>

            {/* Timeline Container */}
            <div className="relative pl-8 border-l-2 border-gradient">
                {section.items.map((item, itemIndex) => (
                    <motion.div
                        key={item.id || itemIndex}
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.5, delay: itemIndex * 0.1 }}
                        className="relative mb-8 last:mb-0"
                    >
                        {/* Timeline Dot */}
                        <div className="absolute -left-[37px] top-2 w-4 h-4 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 ring-4 ring-white dark:ring-gray-900" />

                        {/* Content Card */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
                            {/* Date Badge */}
                            {item.date && (
                                <div className="inline-block px-3 py-1 mb-3 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 rounded-full">
                                    {item.date}
                                </div>
                            )}

                            {/* Title */}
                            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">
                                {item.title}
                            </h3>

                            {/* Subtitle */}
                            {item.subtitle && (
                                <p className="text-gray-600 dark:text-gray-400 font-medium mb-2">
                                    {item.subtitle}
                                </p>
                            )}

                            {/* Description */}
                            {item.description && (
                                <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-3">
                                    {item.description}
                                </p>
                            )}

                            {/* Tags */}
                            {item.tags && item.tags.length > 0 && (
                                <div className="flex flex-wrap gap-2 mt-3">
                                    {item.tags.map((tag, tagIndex) => (
                                        <span
                                            key={tagIndex}
                                            className="px-2 py-1 text-xs font-medium text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-900/30 rounded"
                                        >
                                            {tag}
                                        </span>
                                    ))}
                                </div>
                            )}

                            {/* Link */}
                            {item.link && (
                                <a
                                    href={item.link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center mt-3 text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium"
                                >
                                    View Details →
                                </a>
                            )}
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.section>
    );
}
