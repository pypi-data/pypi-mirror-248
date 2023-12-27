import adapter from '@sveltejs/adapter-static'

const buildDir = 'BUILD_DIR' in process.env ? process.env.BUILD_DIR : 'build'
// console.log('buildDir', buildDir)

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter({
      // See https://kit.svelte.dev/docs/adapter-static
      pages: buildDir,
      // defaults to the same value as pages
      // assets: build_dir,
      fallback: undefined,
      precompress: false,
      strict: true
    }),
    prerender: {
      handleMissingId: 'ignore'
    }
  }
}

export default config
