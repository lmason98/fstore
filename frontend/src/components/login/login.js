import React, { useState } from 'react'
import { Grid, Card, CardContent, CardActions, Button, TextField } from '@mui/material'

function Login({ doLogin }) {

    const [user, setUser] = useState('')
    const [pass, setPass] = useState('')

    const handleUser = (e) => setUser(e.target.value)
    const handlePass = (e) => setPass(e.target.value)
    const handleLogin = () => {
        doLogin(user, pass)
    }

    return (
        <Card variant='outlined'>
            <CardContent>
                <Grid container spacing={1}>
                    <Grid item xs={12}>
                        <TextField sx={{width: '100%'}} label='Username' value={user} onChange={handleUser} />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField sx={{width: '100%'}} label='Password' value={pass} onChange={handlePass} />
                    </Grid>
                </Grid>
            </CardContent>
            <CardActions justifyContent='center'>
                <Button variant='contained' onClick={handleLogin}>Login</Button>
            </CardActions>
        </Card>
    )
}

export default Login