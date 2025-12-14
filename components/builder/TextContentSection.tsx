'use client';

import { motion } from 'framer-motion';
import type { SectionSchema } from '@/lib/schema';

interface TextContentSectionProps {
    section: SectionSchema;
    index: number;
}

/**
 * Text Content Section - Rich text blocks
 * Perfect for: Bio, Research Interests, Teaching Philosophy
 */
export function TextContentSection({ section, index }: TextContentSectionProps) {
    return (
        <motion.section
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
            className="mb-16"
        >
            {/* Section Header */}
            <h2 className="text-3xl font-bold mb-8 bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent">
                {section.title}
            </h2>

            {/* Text Content Container */}
            <div className="space-y-6">
                {section.items.map((item, itemIndex) => (
                    <motion.div
                        key={item.id || itemIndex}
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.5, delay: itemIndex * 0.1 }}
                        className="prose prose-lg dark:prose-invert max-w-none"
                    >
                        {/* Subsection Title (if applicable) */}
                        {item.title && (
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                                {item.title}
                            </h3>
                        )}

                        {/* Subtitle */}
                        {item.subtitle && (
                            <h4 className="text-md font-medium text-gray-700 dark:text-gray-300 mb-2 italic">
                                {item.subtitle}
                            </h4>
                        )}

                        {/* Description - Main Content */}
                        {item.description && (
                            <div className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
                                {item.description}
                            </div>
                        )}

                        {/* Tags as Topic Pills */}
                        {item.tags && item.tags.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-4 not-prose">
                                {item.tags.map((tag, tagIndex) => (
                                    <span
                                        key={tagIndex}
                                        className="px-3 py-1 text-sm font-medium text-teal-700 dark:text-teal-300 bg-teal-100 dark:bg-teal-900/30 rounded-full"
                                    >
                                        {tag}
                                    </span>
                                ))}
                            </div>
                        )}

                        {/* Optional Link */}
                        {item.link && (
                            <a
                                href={item.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center mt-3 text-teal-600 dark:text-teal-400 hover:underline font-medium not-prose"
                            >
                                Learn More →
                            </a>
                        )}
                    </motion.div>
                ))}
            </div>
        </motion.section>
    );
}
