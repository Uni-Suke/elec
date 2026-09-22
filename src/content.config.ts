import {defineCollection} from 'astro:content';
import {z} from 'astro/zod';
import {glob} from 'astro/loaders';
const lessons=defineCollection({
 loader:glob({pattern:'**/*.md',base:'./src/content/lessons'}),
 schema:z.object({
  title:z.string().min(3),description:z.string().min(10),
  category:z.enum(['basics','components','circuits','measurement','experiments','troubleshooting','design']),
  order:z.number().int().nonnegative(),minutes:z.number().positive(),
  level:z.enum(['入門','基礎','実践']).default('基礎'),
  tags:z.array(z.string()).min(1),objectives:z.array(z.string()).min(1),
  related:z.array(z.string()).default([]),
  diagram:z.string().optional(),diagramCaption:z.string().optional(),
  warning:z.string().optional(),
  formula:z.object({expression:z.string(),example:z.string()}).optional(),
  quiz:z.object({question:z.string(),answer:z.string()}),
  reviewed:z.string(),
 })
});
export const collections={lessons};
