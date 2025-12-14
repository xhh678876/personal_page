import { z } from 'zod';

// ============================================================================
// DYNAMIC SCHEMA FOR VISION-BASED ACADEMIC PROFILE PARSER
// ============================================================================

// Social Links Schema
const socialLinkSchema = z.object({
  platform: z.string().describe('Platform name (e.g., GitHub, LinkedIn, Twitter, Google Scholar)'),
  url: z.string().url().describe('Full URL to the profile'),
  username: z.string().optional().describe('Username on the platform'),
});

// Item Schema - Flexible content block that can represent publications, projects, etc.
const sectionItemSchema = z.object({
  id: z.string().optional().describe('Unique identifier for the item'),
  title: z.string().describe('Main title of the item (e.g., paper title, project name)'),
  subtitle: z.string().optional().describe('Secondary info (e.g., venue, company name)'),
  date: z.string().optional().describe('Date or date range (e.g., "2023", "Jan 2022 - Present")'),
  description: z.string().optional().describe('Detailed description or abstract'),
  tags: z.array(z.string()).optional().describe('Tech stack, topics, or keywords'),
  link: z.string().url().optional().describe('External link (DOI, GitHub, website)'),
  image: z.string().url().optional().describe('Associated image or thumbnail URL'),
  metadata: z.record(z.string()).optional().describe('Additional key-value pairs for custom fields'),
});

// Section Type Enum - Determines how the section will be rendered
const sectionTypeSchema = z.enum([
  'timeline',      // Vertical timeline with dates (education, work history)
  'grid-list',     // Card grid layout (publications, projects, patents)
  'text-content',  // Rich text blocks (bio, research statement)
  'gallery',       // Image gallery (posters, lab photos)
]);

// Section Schema - A modular content block
const sectionSchema = z.object({
  id: z.string().describe('Unique identifier for the section'),
  type: sectionTypeSchema.describe('Rendering layout type'),
  title: z.string().describe('Section heading (e.g., "Publications", "Patents", "Teaching")'),
  items: z.array(sectionItemSchema).describe('Array of content items in this section'),
  order: z.number().optional().describe('Display order (lower numbers appear first)'),
});

// Theme Configuration Schema
const themeConfigSchema = z.object({
  style: z.enum(['bento', 'minimal', 'cyber', 'academic']).describe('Overall design aesthetic'),
  accentColor: z.string().optional().describe('Primary accent color (hex or CSS variable)'),
  font: z.string().optional().describe('Font family preference'),
  layout: z.enum(['single-column', 'sidebar', 'split']).optional().describe('Page layout structure'),
});

// Main Profile Schema
export const profileSchema = z.object({
  // Fixed Basics Section
  basics: z.object({
    name: z.string().describe('Full name of the person'),
    label: z.string().describe('Professional title or role (e.g., "PhD Student in AI", "Assistant Professor")'),
    bio: z.string().describe('Brief biography or research interests summary'),
    avatar: z.string().url().optional().describe('Profile photo URL'),
    email: z.string().email().describe('Primary contact email'),
    website: z.string().url().optional().describe('Personal website or homepage'),
    socials: z.array(socialLinkSchema).optional().describe('Social media and academic profiles'),
  }),
  
  // Dynamic Sections Array
  sections: z.array(sectionSchema).describe('Modular content sections detected from the resume'),
  
  // Theme Configuration
  theme: themeConfigSchema.optional().describe('Visual styling preferences'),
});

// ============================================================================
// TYPESCRIPT TYPE EXPORTS
// ============================================================================

export type ProfileSchema = z.infer<typeof profileSchema>;
export type SectionSchema = z.infer<typeof sectionSchema>;
export type SectionItemSchema = z.infer<typeof sectionItemSchema>;
export type SectionType = z.infer<typeof sectionTypeSchema>;
export type SocialLinkSchema = z.infer<typeof socialLinkSchema>;
export type ThemeConfig = z.infer<typeof themeConfigSchema>;
