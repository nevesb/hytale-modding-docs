// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import { readFileSync, writeFileSync } from 'node:fs';
import { readdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>\n';

/** Garante que os sitemaps tenham declaração XML e estejam bem formados para o Google. */
function sitemapPatch() {
	return {
		name: 'sitemap-patch',
		hooks: {
			'astro:build:done': ({ dir }) => {
				const dirPath = fileURLToPath(dir);
				const files = readdirSync(dirPath).filter((f) => f.startsWith('sitemap') && f.endsWith('.xml'));
				for (const file of files) {
					const path = join(dirPath, file);
					let content = readFileSync(path, 'utf-8').trim();
					if (!content.startsWith('<?xml')) {
						content = XML_DECLARATION + content;
					}
					writeFileSync(path, content + '\n', 'utf-8');
				}
			},
		},
	};
}

export default defineConfig({
	site: 'https://nevesb.github.io',
	base: '/hytale-modding-docs',
	integrations: [
		starlight({
			title: 'Hytale Modding Manual',
			logo: { src: './src/assets/logo.png' },
			defaultLocale: 'root',
			head: [
				{
					tag: 'meta',
					attrs: {
						name: 'description',
						content: 'Hytale modding documentation — JSON schemas, NPCs, items, crafting, tutorials. Server modding reference in English, Spanish, Portuguese.',
					},
				},
				{
					tag: 'meta',
					attrs: {
						name: 'robots',
						content: 'index, follow',
					},
				},
				{
					tag: 'script',
					attrs: { type: 'application/ld+json' },
					content: JSON.stringify({
						'@context': 'https://schema.org',
						'@type': 'WebSite',
						name: 'Hytale Modding Manual',
						url: 'https://nevesb.github.io/hytale-modding-docs/',
						description: 'Comprehensive Hytale modding documentation: JSON schemas, NPC system, items, crafting, world config, and step-by-step tutorials. Available in English, Spanish, and Portuguese.',
						potentialAction: {
							'@type': 'SearchAction',
							target: {
								'@type': 'EntryPoint',
								urlTemplate: 'https://nevesb.github.io/hytale-modding-docs/?q={search_term_string}',
							},
							'query-input': 'required name=search_term_string',
						},
					}),
				},
				{
					tag: 'script',
					attrs: { type: 'module' },
					content: `
						import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
						mermaid.initialize({ startOnLoad: false, theme: 'dark' });
						function initMermaid() {
							const pres = document.querySelectorAll('pre[data-language="mermaid"]');
							let found = false;
							pres.forEach((pre) => {
								found = true;
								const code = pre.querySelector('code');
								const text = code ? code.textContent : pre.textContent;
								const div = document.createElement('div');
								div.className = 'mermaid';
								div.textContent = text;
								const wrapper = pre.closest('.expressive-code') || pre.closest('figure') || pre;
								wrapper.replaceWith(div);
							});
							if (found) mermaid.run();
						}
						if (document.readyState === 'loading') {
							document.addEventListener('DOMContentLoaded', initMermaid);
						} else {
							initMermaid();
						}
					`,
				},
			],
			locales: {
				root: { label: 'English', lang: 'en-US' },
				es: { label: 'Español', lang: 'es' },
				'pt-br': { label: 'Português (BR)', lang: 'pt-BR' },
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/nevesb/hytale-modding-docs' },
			],
			customCss: ['./src/styles/home.css'],
			sidebar: [
				{
					label: 'Getting Started',
					translations: {
						es: 'Primeros Pasos',
						'pt-BR': 'Primeiros Passos',
					},
					autogenerate: { directory: 'getting-started' },
				},
				{
					label: 'Reference',
					translations: {
						es: 'Referencia',
						'pt-BR': 'Referência',
					},
					items: [
						{
							label: 'Concepts',
							translations: { es: 'Conceptos', 'pt-BR': 'Conceitos' },
							autogenerate: { directory: 'reference/concepts' },
						},
						{
							label: 'NPC System',
							translations: { es: 'Sistema de NPC', 'pt-BR': 'Sistema de NPC' },
							autogenerate: { directory: 'reference/npc-system' },
						},
						{
							label: 'Item System',
							translations: { es: 'Sistema de Items', 'pt-BR': 'Sistema de Itens' },
							autogenerate: { directory: 'reference/item-system' },
						},
						{
							label: 'Crafting System',
							translations: { es: 'Sistema de Crafteo', 'pt-BR': 'Sistema de Crafting' },
							autogenerate: { directory: 'reference/crafting-system' },
						},
						{
							label: 'Combat & Projectiles',
							translations: { es: 'Combate y Proyectiles', 'pt-BR': 'Combate e Projéteis' },
							autogenerate: { directory: 'reference/combat-and-projectiles' },
						},
						{
							label: 'Economy & Progression',
							translations: { es: 'Economía y Progresión', 'pt-BR': 'Economia e Progressão' },
							autogenerate: { directory: 'reference/economy-and-progression' },
						},
						{
							label: 'World & Environment',
							translations: { es: 'Mundo y Entorno', 'pt-BR': 'Mundo e Ambiente' },
							autogenerate: { directory: 'reference/world-and-environment' },
						},
						{
							label: 'Models & Visuals',
							translations: { es: 'Modelos y Visuales', 'pt-BR': 'Modelos e Visuais' },
							autogenerate: { directory: 'reference/models-and-visuals' },
						},
						{
							label: 'Game Configuration',
							translations: { es: 'Configuración del Juego', 'pt-BR': 'Configuração do Jogo' },
							autogenerate: { directory: 'reference/game-configuration' },
						},
					],
				},
				{
					label: 'Tutorials',
					translations: {
						es: 'Tutoriales',
						'pt-BR': 'Tutoriais',
					},
					items: [
						{
							label: 'Beginner',
							translations: { es: 'Principiante', 'pt-BR': 'Iniciante' },
							autogenerate: { directory: 'tutorials/beginner' },
						},
						{
							label: 'Intermediate',
							translations: { es: 'Intermedio', 'pt-BR': 'Intermediário' },
							autogenerate: { directory: 'tutorials/intermediate' },
						},
						{
							label: 'Advanced',
							translations: { es: 'Avanzado', 'pt-BR': 'Avançado' },
							autogenerate: { directory: 'tutorials/advanced' },
						},
						{
							label: 'Showcase',
							translations: { es: 'Ejemplos', 'pt-BR': 'Exemplos' },
							autogenerate: { directory: 'tutorials/showcase' },
						},
					],
				},
			],
		}),
		sitemap(),
		sitemapPatch(),
	],
});
