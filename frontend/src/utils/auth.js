/**
 * File: auth.tsx
 * Desc: Holds auth token for the app
 */
import api, { apiURL } from './api'

const responseText404 = 'Not found.'
const responseText403 = 'Forbidden, insufficient permissions.'

// This inserts the auth token into every axios request if it exists
api.interceptors.request.use(config => {
    const authService = new AuthService()

    if (config.headers === undefined)
      config.headers = {}

    if (config.baseURL === apiURL && !config.headers.Authorization) {
      const token = authService.getToken()

      if (token)
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
)
// This parses errors on responses to axios
api.interceptors.response.use(resp => {
  return resp
}, error => {
  if (error.response) {
    if (401 === error.response.status)
      error.response['data'] = {message: error.response.data?.message}
    else if (403 === error.response.status)
      error.response['data'] = {message: responseText403}
    else if (404 === error.response.status)
      error.response['data'] = {message: responseText404}

    return Promise.reject(error)
  } else
    return Promise.reject(error)
})

class AuthService {

  login(user, pass) {
  	return api.post('/auth/token/obtain', {
      username: user,
      password: pass
  	}).then(resp => {
      if (resp.data.status === 'success') {
        this.setToken(resp.data.access)
        this.setRefreshToken(resp.data.refresh)
        this.setUserId(resp.data.userId)
        this.setUserName(user)
        return Promise.resolve(resp)
      } else {
        this.logout()
        return Promise.reject(resp)
      }
    }).catch(err => {
      return Promise.reject(err)
    })
  }

  check() {
    return api.get('/auth/token/check')
      .then(resp => {
        if (resp.data.status === 'success')
          return Promise.resolve(resp)
        else
          return Promise.reject(resp)
      })
  }

  logout() {
    this.setToken('')
    this.setRefreshToken('')
    this.setUserId('')
    this.setUserName('')
  }

  isAuthed() {
    return !!(this.getToken() && this.getToken() !== '' && this.getRefreshToken() && this.getRefreshToken() !== '')
  }

  setUserName(name) {
    localStorage.setItem('userName', name)
  }

  setUserId(id) {
    localStorage.setItem('userId', id)
  }

  setToken(token) {
  	localStorage.setItem('idToken', token)
  }

  getToken() {
    return localStorage.getItem('idToken')
  }

  setRefreshToken(token) {
  	localStorage.setItem('idTokenRefresh', token)
  }

  getRefreshToken() {
  	return localStorage.getItem('idTokenRefresh')
  }

  refresh() {
    if (this.getRefreshToken() === null) return Promise.reject('No refresh token in memory')

    return api.post('/auth/token/refresh', {
      refresh: this.getRefreshToken()
    }).then((resp) => {
      this.setToken(resp.data.access)
      this.setRefreshToken(resp.data.refresh)
      return Promise.resolve(resp)
    }).catch((err) => {
      this.logout()
      return Promise.reject(err)
    })
  }
}

const getUserId = () => localStorage.getItem('userId')
const getUserName = () => localStorage.getItem('userName')

export default AuthService
export {
  getUserId,
  getUserName
}
