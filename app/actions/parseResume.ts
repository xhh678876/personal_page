'use server';

import { generateObject } from 'ai';
import { createOpenAI } from '@ai-sdk/openai';
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { profileSchema } from '@/lib/schema';
import type { ProfileSchema } from '@/lib/schema';

interface ParseResumeInput {
    images: string[];  // Base64 data URLs
    apiKey: string;
    provider: 'openai' | 'gemini';
}

interface ParseResumeResult {
    success: boolean;
    data?: ProfileSchema;
    error?: string;
}

/**
 * Vision-based Server Action for parsing academic resumes/CVs
 * Supports OpenAI (gpt-4o) and Google (gemini-2.0-flash-exp) Vision models
 * 
 * @param input - Images (base64), API key, and provider selection
 * @returns Parsed profile data or error message
 */
export async function parseResumeAction(
    input: ParseResumeInput
): Promise<ParseResumeResult> {
    const { images, apiKey, provider } = input;

    // Validate inputs
    if (!images || images.length === 0) {
        return {
            success: false,
            error: 'No images provided. Please upload a PDF first.',
        };
    }

    if (!apiKey || apiKey.trim().length === 0) {
        return {
            success: false,
            error: 'API key is required.',
        };
    }

    // Basic API key format validation
    if (provider === 'openai' && !apiKey.startsWith('sk-')) {
        return {
            success: false,
            error: 'Invalid OpenAI API key format. Keys should start with "sk-".',
        };
    }

    if (provider === 'gemini' && !apiKey.startsWith('AIzaSy')) {
        return {
            success: false,
            error: 'Invalid Google API key format. Keys should start with "AIzaSy".',
        };
    }

    try {
        // Vision-optimized prompt for academic resume parsing
        const systemPrompt = `You are an expert academic CV/resume parser with deep knowledge of academic formats, publication venues, and research structures.

Your task is to analyze the provided resume/CV images VISUALLY and extract ALL information into a structured format.

CRITICAL INSTRUCTIONS:
1. **Basic Information**: Extract name, professional title/label, email, website, and write a concise bio summarizing their research focus.

2. **Section Detection**: Identify ALL distinct sections in the CV. Common sections include:
   - Education
   - Publications (journals, conferences, preprints)
   - Research Experience / Work History
   - Projects
   - Awards & Honors
   - Patents
   - Talks & Presentations
   - Teaching
   - Service
   - Skills
   - Certifications
   
   BUT ALSO look for UNCOMMON sections like:
   - Exhibitions (for artists/designers)
   - Performances
   - Media Coverage
   - Grants & Funding
   - Collaborations
   
3. **Section Type Classification**: For each section, choose the BEST layout type:
   - 'timeline': Use for chronological sequences (Education, Work History, Awards with dates)
   - 'grid-list': Use for collections of discrete items (Publications, Projects, Patents, Talks)
   - 'text-content': Use for paragraph-style content (Bio, Research Interests, Teaching Philosophy)
   - 'gallery': Use if there are visual elements like posters, charts, or photos
   
4. **Content Extraction**: For each item:
   - Extract title, subtitle (venue/company), dates
   - Write descriptions when available
   - Extract tags: For publications, include topics/keywords. For projects, include tech stack.
   - Capture links (DOI, GitHub, personal sites)
   - Extract author lists for publications (preserve order)
   - Normalize dates to consistent formats
   
5. **Metadata Handling**: Use the 'metadata' field for special information:
   - For publications: { "citations": "123", "impact_factor": "4.5", "type": "conference" }
   - For projects: { "role": "Lead Developer", "team_size": "5" }
   
6. **Ordering**: Assign order numbers to sections based on their importance/appearance in CV.

7. **Theme Inference**: Based on the CV's visual design, suggest a theme style:
   - 'academic': Traditional, formal CVs
   - 'minimal': Clean, modern layouts
   - 'cyber': Technical, developer-focused
   - 'bento': Modern, card-based designs

RETURN ONLY the structured JSON matching the schema. Be thorough and precise.`;

        // Prepare Vision API messages with multi-image input
        const imageMessages = images.map((imageUrl) => ({
            type: 'image' as const,
            image: imageUrl,
        }));

        let result;

        if (provider === 'openai') {
            // Initialize OpenAI provider with user's API key at runtime (BYOK)
            const openai = createOpenAI({
                apiKey: apiKey,
            });

            result = await generateObject({
                model: openai('gpt-4o'),
                schema: profileSchema,
                messages: [
                    {
                        role: 'system',
                        content: systemPrompt,
                    },
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'text',
                                text: 'Please analyze this academic CV/resume and extract all information following the instructions.',
                            },
                            ...imageMessages,
                        ],
                    },
                ],
                temperature: 0.1,
            });
        } else if (provider === 'gemini') {
            // Initialize Google Gemini provider with user's API key
            const google = createGoogleGenerativeAI({
                apiKey: apiKey,
            });

            result = await generateObject({
                model: google('gemini-2.0-flash-exp'),
                schema: profileSchema,
                messages: [
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'text',
                                text: systemPrompt + '\n\nPlease analyze this academic CV/resume and extract all information following the instructions.',
                            },
                            ...imageMessages,
                        ],
                    },
                ],
                temperature: 0.1,
            });
        } else {
            return {
                success: false,
                error: 'Unsupported provider. Please use "openai" or "gemini".',
            };
        }

        return {
            success: true,
            data: result.object,
        };
    } catch (err) {
        console.error('Vision parsing error:', err);

        // Handle specific error types
        if (err instanceof Error) {
            if (err.message.includes('API key') || err.message.includes('API_KEY')) {
                return {
                    success: false,
                    error: 'Invalid API key. Please check your key and try again.',
                };
            }
            if (err.message.includes('rate limit')) {
                return {
                    success: false,
                    error: 'Rate limit exceeded. Please wait a moment and try again.',
                };
            }
            if (err.message.includes('insufficient_quota') || err.message.includes('quota')) {
                return {
                    success: false,
                    error: 'API quota exceeded. Please check your account.',
                };
            }
            if (err.message.includes('billing')) {
                return {
                    success: false,
                    error: 'Billing not enabled. Please enable billing for your API key.',
                };
            }

            return {
                success: false,
                error: `Parsing failed: ${err.message}`,
            };
        }

        return {
            success: false,
            error: 'An unknown error occurred during parsing.',
        };
    }
}
