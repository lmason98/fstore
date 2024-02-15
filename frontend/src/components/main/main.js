import React, { useState, useEffect } from 'react'
import { Grid, Box, Typography, Button, CircularProgress } from '@mui/material'
import { useAlert } from '../alert/alert'
import Login from '../login/login'

function Main() {
    const alert = useAlert()

    const [authed, setAuthed] = useState(false)
    const [loading, setLoading] = useState(true)

    const doLogin = (user, pass) => {
        alert(`Attempt to login ${user}`, 'success')
        setAuthed(true)
    }

    useEffect(() => {
        setLoading(false)
    })

    return (
        <>
            {loading ?
                <Box sx={{display: 'flex', textAlign: 'center', height: '100vh'}}>
                    <CircularProgress sx={{margin: 'auto auto'}} />
                </Box>
            :
                authed ?
                    <Box sx={{display: 'flex', textAlign: 'center', height: '100vh'}}>
                        <Typography sx={{margin: 'auto auto'}}>You are authed!</Typography>
                    </Box>
                :
                    <Grid
                        container
                        spacing={0}
                        direction='column'
                        alignItems='center'
                        justifyContent='center'
                        sx={{display: 'flex', textAlign: 'center', height: '100vh'}}
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