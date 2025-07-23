import { defineStore } from 'pinia'
import axios from 'axios'

export const useApiStore = defineStore('api', {
  state: () => ({
    baseURL: '/api',
    isConnected: false,
  }),

  actions: {
    async testConnection() {
      try {
        const response = await axios.get(`${this.baseURL}/health`)
        this.isConnected = true
        return response.data
      } catch (error) {
        this.isConnected = false
        throw error
      }
    },

    async getApiInfo() {
      try {
        const response = await axios.get(`${this.baseURL}/v1/`)
        return response.data
      } catch (error) {
        throw error
      }
    },

    async getClients() {
      try {
        const response = await axios.get(`${this.baseURL}/v1/clients`)
        return response
      } catch (error) {
        throw error
      }
    }
  }
})