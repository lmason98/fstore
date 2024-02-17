import {
  Box,
  Button,
  Divider,
  Drawer,
  List,
  ListItem, ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography
} from '@mui/material'
import ListIcon from '@mui/icons-material/List'

import Content from '../content/content'
import { getUserName } from '../../utils/auth'

const drawerWidth = 240

const links = [
  {text: 'My Files', icon: <ListIcon />}
]

function Navigation({ logout }) {
  return (
    <Box sx={{display: 'flex'}}>
      <Drawer variant='permanent' anchor='left' sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}>
        <Toolbar>
          <Typography variant='h4'>File Store</Typography>
        </Toolbar>
        <Divider />
        <List sx={{height: '100%', display: 'flex', flexDirection: 'column'}}>
          {links.map((link, key) => (
            <ListItem disablePadding key={key}>
              <ListItemButton>
                <ListItemIcon>
                  {link.icon}
                </ListItemIcon>
                <ListItemText primary={link.text} />
              </ListItemButton>
            </ListItem>
          ))}
          <ListItem sx={{marginTop: 'auto', display: 'flex'}}>
            <Button sx={{margin: 'auto auto'}} variant='contained' onClick={logout}>Logout {getUserName()}</Button>
          </ListItem>
        </List>
      </Drawer>

      {/* Main app content */}
      <Content />

    </Box>
  )
}

export default Navigation