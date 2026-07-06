import { defineStore } from 'pinia'

export const useSiteStore = defineStore('site', {
  state: () => ({
    settings: {
      logo_kr: '하이어 프로덕션',
      logo_en: 'HIGHER PRODUCTION',
      about_headings: [],
      email: '',
      phone: '',
      address: '',
      instagram_handle: '',
      instagram_url: '',
      contact_title: '',
      footer_slogan_main: [],
      footer_slogan_sub: '',
      
      is_service_visible: true,
      service_title: 'MONTHLY PLAN',
      service_desc: '영상 운영 가격 / 한달 기준',
      
      is_about_visible: true,
      about_title: 'ABOUT THE STUDIO',
      about_desc: '하이어, 더 높은 곳으로',
      
      is_contact_visible: true,
      contact_header_title: 'GET IN TOUCH',
      contact_header_desc: '하이어, 더 높은 곳으로'
    },
    isLoaded: false
  }),
  actions: {
    async fetchSettings() {
      if (this.isLoaded) return;
      try {
        const data = await $fetch('http://127.0.0.1:8000/system/settings/')
        if (data) {
          if (data.footer_slogan_main && !Array.isArray(data.footer_slogan_main)) {
            data.footer_slogan_main = [data.footer_slogan_main];
          }
          this.settings = { ...this.settings, ...data }
          this.isLoaded = true
        }
      } catch (e) {
        console.error('Failed to load site settings:', e)
      }
    }
  }
})
