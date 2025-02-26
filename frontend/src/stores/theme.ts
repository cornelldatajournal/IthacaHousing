import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: 'auto' as 'auto' | 'light' | 'dark'
  }),
  actions: {
    fetch() {
      const savedTheme = localStorage.getItem('theme') as 'auto' | 'light' | 'dark' | null;
      this.theme = savedTheme || 'auto';
      this.change(this.theme);
      console.debug(this.theme);
    },
    /**
     * Change the theme
     * @param theme - The theme to change to ('auto', 'light', or 'dark')
     */
    change(theme: 'auto' | 'light' | 'dark') {
      this.theme = theme;
      const isDarkMode =  
        this.theme === 'dark' || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches && this.theme === 'auto');
      document.body.classList.toggle('dark', isDarkMode);
      localStorage.setItem('theme', theme);
    }
  }
});
