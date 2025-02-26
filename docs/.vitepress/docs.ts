import constants from './constants'

export const docsConfig = {
  title: constants.title,
  description: "My notes collections.",
  lang: 'zh',
  lastUpdated: true, // Enable last updated display
  base: constants.base_url,
  srcDir: '.',
  /* Router Config */
  cleanUrls: true,
  rewrites: {},
}
