import React, { useState } from 'react'
import {Grid, Card, CardContent, CardActions, Button, TextField, Typography} from '@mui/material'

function Login({ doLogin }) {

  const [user, setUser] = useState('')
  const [pass, setPass] = useState('')

  const handleUser = (e) => setUser(e.target.value)
  const handlePass = (e) => setPass(e.target.value)
  const handleLogin = () => {
    doLogin(user, pass)
  }

  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <Grid item>
            <Typography variant='h5'>FStore Login</Typography>
          </Grid>
          <Grid item xs={12}>
            <TextField sx={{width: '100%'}} label='Username' value={user} onChange={handleUser} />
          </Grid>
          <Grid item xs={12}>
            <TextField sx={{width: '100%'}} label='Password' value={pass} type='password' onChange={handlePass} />
          </Grid>
        </Grid>
      </CardContent>
      <CardActions sx={{margin: 0.5}}>
        <Button variant='contained' onClick={handleLogin}>Login</Button>
      </CardActions>
    </Card>
  )
}

export default Login