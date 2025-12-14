'use client';

import { motion } from 'framer-motion';
import type { ProfileSchema } from '@/lib/schema';
import { SectionRenderer } from './SectionRenderer';

interface PageBuilderProps {
    profile: ProfileSchema;
}

/**
 * Page Builder - Main orchestrator for rendering dynamic academic homepage
 * Renders basics (hero) section and all dynamic sections
 */
export function PageBuilder({ profile }: PageBuilderProps) {
    const { basics, sections, theme } = profile;

    // Sort sections by order if specified
    const sortedSections = [...sections].sort((a, b) => {
        return (a.order ?? 999) - (b.order ?? 999);
    });

    return (
        <div className={`min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800`}>
            {/* Hero Section (Basics) */}
            <motion.header
                initial={{ opacity: 0, y: -30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="relative overflow-hidden bg-white dark:bg-gray-800 shadow-xl"
            >
                <div className="max-w-6xl mx-auto px-6 py-16 md:py-24">
                    <div className="flex flex-col md:flex-row items-center gap-8">
                        {/* Avatar */}
                        {basics.avatar && (
                            <motion.div
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{ duration: 0.6, delay: 0.2 }}
                                className="relative"
                            >
                                <div className="w-40 h-40 md:w-48 md:h-48 rounded-full overflow-hidden ring-4 ring-purple-500 shadow-2xl">
                                    <img
                                        src={basics.avatar}
                                        alt={basics.name}
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full blur-lg opacity-30 -z-10" />
                            </motion.div>
                        )}

                        {/* Info */}
                        <div className="flex-1 text-center md:text-left">
                            <motion.h1
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6, delay: 0.3 }}
                                className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-2"
                            >
                                {basics.name}
                            </motion.h1>

                            <motion.p
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6, delay: 0.4 }}
                                className="text-xl text-purple-600 dark:text-purple-400 font-semibold mb-4"
                            >
                                {basics.label}
                            </motion.p>

                            <motion.p
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6, delay: 0.5 }}
                                className="text-gray-700 dark:text-gray-300 leading-relaxed max-w-2xl mb-6"
                            >
                                {basics.bio}
                            </motion.p>

                            {/* Contact & Links */}
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.6, delay: 0.6 }}
                                className="flex flex-wrap gap-4 justify-center md:justify-start"
                            >
                                <a
                                    href={`mailto:${basics.email}`}
                                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium"
                                >
                                    📧 Email
                                </a>
                                {basics.website && (
                                    <a
                                        href={basics.website}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors font-medium"
                                    >
                                        🌐 Website
                                    </a>
                                )}
                            </motion.div>

                            {/* Social Links */}
                            {basics.socials && basics.socials.length > 0 && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ duration: 0.6, delay: 0.7 }}
                                    className="flex flex-wrap gap-3 mt-6 justify-center md:justify-start"
                                >
                                    {basics.socials.map((social, idx) => (
                                        <a
                                            key={idx}
                                            href={social.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-gray-600 dark:text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors text-sm"
                                        >
                                            {social.platform}
                                        </a>
                                    ))}
                                </motion.div>
                            )}
                        </div>
                    </div>
                </div>
            </motion.header>

            {/* Dynamic Sections */}
            <main className="max-w-6xl mx-auto px-6 py-12">
                {sortedSections.map((section, index) => (
                    <SectionRenderer key={section.id} section={section} index={index} />
                ))}
            </main>

            {/* Footer */}
            <footer className="bg-gray-800 dark:bg-gray-900 text-gray-400 text-center py-8">
                <p className="text-sm">
                    Generated with Vision AI • Theme: {theme?.style || 'default'}
                </p>
            </footer>
        </div>
    );
}
