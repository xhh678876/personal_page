'use client';

import { useState } from 'react';
import { usePdfToImage } from '@/hooks/usePdfToImage';
import { parseResumeAction } from '@/app/actions/parseResume';
import { PageBuilder } from '@/components/builder/PageBuilder';
import type { ProfileSchema } from '@/types/profile';
import { motion, AnimatePresence } from 'framer-motion';

type Provider = 'openai' | 'gemini';

export default function HomePage() {
    const [profile, setProfile] = useState<ProfileSchema | null>(null);
    const [apiKey, setApiKey] = useState('');
    const [provider, setProvider] = useState<Provider>('gemini');
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [progress, setProgress] = useState<string>('');

    const { convertPdfToImages, loading: converting } = usePdfToImage();

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        if (!apiKey.trim()) {
            setError('请输入 API Key');
            return;
        }

        setError(null);
        setIsProcessing(true);
        setProgress('准备中...');

        try {
            // 1. 转换 PDF 为图片
            setProgress('📄 正在转换 PDF 为图片...');
            const images = await convertPdfToImages(file);
            setProgress(`✅ 已转换 ${images.length} 页，准备发送到 AI...`);

            await new Promise(resolve => setTimeout(resolve, 800));

            // 2. 调用 Vision API 解析
            setProgress(`🤖 正在使用 ${provider === 'gemini' ? 'Gemini 2.5 Pro' : 'GPT-4o'} 分析简历...`);
            const result = await parseResumeAction({
                images,
                apiKey,
                provider,
            });

            if (result.success && result.data) {
                setProgress('✨ 解析成功！正在渲染网站...');
                await new Promise(resolve => setTimeout(resolve, 500));
                setProfile(result.data);
            } else {
                setError(result.error || '解析失败');
            }
        } catch (err) {
            console.error('上传错误:', err);
            setError(err instanceof Error ? err.message : '未知错误');
        } finally {
            setIsProcessing(false);
            setProgress('');
        }
    };

    // 如果已有数据，显示生成的主页
    if (profile) {
        return (
            <div>
                <motion.button
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    onClick={() => setProfile(null)}
                    className="fixed top-4 right-4 z-50 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl font-semibold"
                >
                    ← 返回上传
                </motion.button>
                <PageBuilder profile={profile} />
            </div>
        );
    }

    // 软件风格的上传界面
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
            {/* 背景动画效果 */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute w-96 h-96 bg-purple-500/20 rounded-full blur-3xl -top-48 -left-48 animate-pulse" />
                <div className="absolute w-96 h-96 bg-blue-500/20 rounded-full blur-3xl -bottom-48 -right-48 animate-pulse delay-1000" />
            </div>

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="relative bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-8 md:p-12 max-w-3xl w-full border border-white/20"
            >
                {/* 软件标题栏 */}
                <div className="flex items-center justify-between mb-8 pb-6 border-b border-white/10">
                    <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-2xl">
                            🎓
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-white">学术主页生成器</h1>
                            <p className="text-sm text-gray-300">AI-Powered Academic Website Builder</p>
                        </div>
                    </div>
                    <div className="text-xs text-gray-400">v2.0 Pro</div>
                </div>

                {/* AI 提供商选择 */}
                <div className="mb-6">
                    <label className="block text-sm font-semibold text-white mb-3">
                        选择 AI 提供商
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => setProvider('gemini')}
                            className={`p-4 rounded-xl border-2 transition-all ${provider === 'gemini'
                                    ? 'border-purple-500 bg-purple-500/20'
                                    : 'border-white/20 bg-white/5 hover:bg-white/10'
                                }`}
                        >
                            <div className="flex items-center space-x-3">
                                <div className="text-3xl">✨</div>
                                <div className="text-left">
                                    <div className="font-bold text-white">Google Gemini</div>
                                    <div className="text-xs text-gray-400">2.0 Flash Exp</div>
                                </div>
                            </div>
                            {provider === 'gemini' && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="mt-2 text-xs text-purple-300 font-medium"
                                >
                                    ✓ 已选择（推荐）
                                </motion.div>
                            )}
                        </motion.button>

                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => setProvider('openai')}
                            className={`p-4 rounded-xl border-2 transition-all ${provider === 'openai'
                                    ? 'border-blue-500 bg-blue-500/20'
                                    : 'border-white/20 bg-white/5 hover:bg-white/10'
                                }`}
                        >
                            <div className="flex items-center space-x-3">
                                <div className="text-3xl">🤖</div>
                                <div className="text-left">
                                    <div className="font-bold text-white">OpenAI</div>
                                    <div className="text-xs text-gray-400">GPT-4o Vision</div>
                                </div>
                            </div>
                            {provider === 'openai' && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="mt-2 text-xs text-blue-300 font-medium"
                                >
                                    ✓ 已选择
                                </motion.div>
                            )}
                        </motion.button>
                    </div>
                </div>

                {/* API Key 输入 */}
                <div className="mb-6">
                    <label className="block text-sm font-semibold text-white mb-3">
                        {provider === 'gemini' ? 'Google AI API Key' : 'OpenAI API Key'}
                    </label>
                    <input
                        type="password"
                        placeholder={provider === 'gemini' ? 'AIzaSy...' : 'sk-proj-...'}
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white placeholder-gray-400 transition-all backdrop-blur-sm"
                    />
                    <p className="mt-2 text-xs text-gray-400 flex items-center space-x-1">
                        <span>🔒</span>
                        <span>您的 API Key 仅用于本次解析，不会被存储</span>
                    </p>
                    {provider === 'gemini' && (
                        <a
                            href="https://aistudio.google.com/app/apikey"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-2 inline-block text-xs text-purple-400 hover:text-purple-300 underline"
                        >
                            还没有 API Key？点击这里免费获取 →
                        </a>
                    )}
                </div>

                {/* 文件上传区 */}
                <div className="mb-6">
                    <label className="block text-sm font-semibold text-white mb-3">
                        上传简历 PDF
                    </label>
                    <div className="relative group">
                        <input
                            type="file"
                            accept=".pdf"
                            onChange={handleFileUpload}
                            disabled={isProcessing || converting}
                            className="w-full px-6 py-8 border-2 border-dashed border-white/30 rounded-xl cursor-pointer hover:border-purple-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed bg-white/5 backdrop-blur-sm text-white file:mr-4 file:py-2 file:px-6 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-purple-500 file:to-blue-500 file:text-white hover:file:from-purple-600 hover:file:to-blue-600 file:transition-all file:cursor-pointer"
                        />
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                            <div className="text-center">
                                <div className="text-4xl mb-2">📤</div>
                                <p className="text-sm text-gray-300">点击选择文件或拖拽到此处</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* 处理状态 */}
                <AnimatePresence>
                    {(converting || isProcessing) && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="mb-6 p-4 bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-500/30 rounded-xl backdrop-blur-sm"
                        >
                            <div className="flex items-center space-x-3">
                                <div className="relative">
                                    <div className="w-6 h-6 border-3 border-purple-500 border-t-transparent rounded-full animate-spin" />
                                    <div className="absolute inset-0 w-6 h-6 border-3 border-blue-500 border-t-transparent rounded-full animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1s' }} />
                                </div>
                                <div className="flex-1">
                                    <p className="text-white font-medium text-sm">{progress}</p>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* 错误提示 */}
                <AnimatePresence>
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl backdrop-blur-sm"
                        >
                            <p className="text-red-300 text-sm flex items-center space-x-2">
                                <span>❌</span>
                                <span>{error}</span>
                            </p>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* 功能说明 */}
                <div className="p-6 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
                    <h3 className="text-sm font-semibold text-white mb-3 flex items-center space-x-2">
                        <span>💡</span>
                        <span>使用指南</span>
                    </h3>
                    <ul className="text-xs text-gray-300 space-y-2">
                        <li className="flex items-start space-x-2">
                            <span className="text-purple-400 mt-0.5">▸</span>
                            <span><strong>推荐使用 Gemini</strong> - 免费额度更多，响应更快</span>
                        </li>
                        <li className="flex items-start space-x-2">
                            <span className="text-purple-400 mt-0.5">▸</span>
                            <span>支持任意学术简历格式（单列、双列、创意设计）</span>
                        </li>
                        <li className="flex items-start space-x-2">
                            <span className="text-purple-400 mt-0.5">▸</span>
                            <span>AI 自动识别教育、出版物、项目等所有章节</span>
                        </li>
                        <li className="flex items-start space-x-2">
                            <span className="text-purple-400 mt-0.5">▸</span>
                            <span>解析时间约 10-30 秒（取决于页数和模型）</span>
                        </li>
                        <li className="flex items-start space-x-2">
                            <span className="text-purple-400 mt-0.5">▸</span>
                            <span>建议 PDF 不超过 10 页（成本优化）</span>
                        </li>
                    </ul>
                </div>

                {/* Footer */}
                <div className="mt-8 pt-6 border-t border-white/10 text-center text-xs text-gray-400">
                    <p>Powered by Gemini 2.0 / GPT-4o Vision • Next.js 14 • Tailwind CSS</p>
                    <p className="mt-1">Made with ❤️ for Researchers</p>
                </div>
            </motion.div>
        </div>
    );
}
