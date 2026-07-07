import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const accessToken = ref(null)
    const refreshToken = ref(null)

    const login = async (username, password) => {
        try {
            // Nuxt 내장 $fetch를 사용하여 Django(8000포트)와 통신
            const response = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/account/login/', {
                method: 'POST',
                body: {
                    username,
                    password
                }
            })
            
            // 로그인 성공 시 백엔드에서 받은 데이터 저장
            user.value = response.user
            accessToken.value = response.access_token
            refreshToken.value = response.refresh_token
            
            return { success: true }
        } catch (error) {
            console.error('Login error:', error)
            // 백엔드에서 보내준 에러 메시지(error) 추출
            const errorMsg = error.response?._data?.error || '서버와 통신할 수 없습니다.'
            return { success: false, message: errorMsg }
        }
    }

    const logout = () => {
        user.value = null
        accessToken.value = null
        refreshToken.value = null
    }

    return { user, accessToken, refreshToken, login, logout }
}, {
    // pinia-plugin-persistedstate: 새로고침해도 로그인이 유지되도록 로컬스토리지에 저장합니다.
    persist: true 
})
