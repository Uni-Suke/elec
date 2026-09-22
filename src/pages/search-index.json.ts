import {getCollection} from 'astro:content';
export async function GET(){const lessons=await getCollection('lessons');return new Response(JSON.stringify(lessons.map(e=>({id:e.id,...e.data,body:e.body||''}))),{headers:{'Content-Type':'application/json; charset=utf-8'}});}
