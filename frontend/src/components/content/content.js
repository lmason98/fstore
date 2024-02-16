import { Box, Grid, Typography } from '@mui/material'
import Upload from '../upload/upload'


function Content() {
  return (
    <Box sx={{display: 'flex', width: '100%'}}>
      <Grid
        container
        spacing={0}
        direction='column'
        sx={{height: '100vh', backgroundColor: '#eaeaea'}}
      >
        <Grid item container spacing={10}>
          <Grid item>
            <Typography>You are authed!</Typography>
            <Upload />
          </Grid>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Content