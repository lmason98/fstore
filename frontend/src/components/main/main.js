import React, { useState, useEffect } from 'react'
import { Grid, Box, Typography, CircularProgress, Button } from '@mui/material'

import { useAlert } from '../alert/alert'
import Login from '../login/login'
import AuthService from '../../utils/auth'
import api from '../../utils/api'

const authService = new AuthService()

function Main() {
  const alert = useAlert()

  const [authed, setAuthed] = useState(false)
  const [loading, setLoading] = useState(true)

  const doLogin = (user, pass) => {
    authService.login(user, pass)
      .then(resp => {
        alert(resp.data.message, resp.data.status)
        setAuthed(true)
      })
      .catch(err => alert(err.data.message, err.data.status))
  }

  const doLogout = () => {
    setAuthed(false)
    authService.logout()
  }

  useEffect(() => {
    authService.check()
      .then(() => {
        setLoading(false)
        setAuthed(true)
      })
      .catch(() => {
        setLoading(false)
        setAuthed(false)
      })
  })

  return (
    <>
      {loading ?
        <Box sx={{display: 'flex', textAlign: 'center', height: '100vh'}}>
          <CircularProgress sx={{margin: 'auto auto'}} />
        </Box>
      :
        authed ?
          <Grid
            container
            spacing={0}
            direction='column'
            alignItems='center'
            justifyContent='center'
            sx={{display: 'flex', height: '100vh', backgroundColor: '#eaeaea'}}
          >
            <Grid item>
              <Typography sx={{margin: 'auto auto'}}>You are authed!</Typography>
            </Grid>
            <Grid item>
              <Button variant='contained' onClick={doLogout}>Logout</Button>
            </Grid>
          </Grid>
        :
          <Grid
            container
            spacing={0}
            direction='column'
            alignItems='center'
            justifyContent='center'
            sx={{display: 'flex', height: '100vh', backgroundColor: '#eaeaea'}}
          >
            <Grid item>
              <Login doLogin={doLogin} />
            </Grid>
          </Grid>
      }
    </>
  )
}

export default Main