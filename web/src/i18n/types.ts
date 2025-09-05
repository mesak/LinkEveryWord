export type Lang = 'zh' | 'en'

export interface Dict {
  common: {
    brand: string
  nav: { home: string; chrome: string; desktop: string; privacy: string; github: string; lang: string; donate: string }
  }
  home: {
    title: string
    intro: string
    quickStart: string
    items: { chrome: string; desktop: string }
  }
  chrome: {
    title: string
    installFromStore: string
    steps: string[]
    usageTitle: string
    usageItems: string[]
    privacyNote: string
    detailsNote: string
  }
  desktop: {
    title: string
    method1: string[]
    method2: string[]
    reqTitle: string
    reqList: string[]
    more: string
  }
  privacy: {
    title: string
    enNotice?: string
  }
}
