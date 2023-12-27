import fontAwesomeIconGenerator from 'font-awesome-icon-generator'

const config = {
  iconOutputFile: (size) => `static/favicon.png`,
  unicodeHex: 'f017',
  sizes: [128],
  color: '#1467eb',
  mirrorX: true,
}

await fontAwesomeIconGenerator(config)