import React, { useState } from 'react'
import {Button, ListItemIcon, ListItemText, Menu, MenuItem} from '@mui/material'
import { ExpandMore } from '@mui/icons-material'

function ActionList({ objectInfo, actions }) {
  const [anchorEl, setAnchorEl] = useState(null)
  const open = Boolean(anchorEl)

  const { id, type, name } = objectInfo

  const handleClick = (e) => setAnchorEl(e.currentTarget)
  const handleClose = () => setAnchorEl(null)

  return (
    <div>
      <Button
        startIcon={<ExpandMore />}
        variant='contained'
        aria-controls={open ? 'basic-menu' : undefined}
        aria-haspopup='true'
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
      >
        Actions
      </Button>
      <Menu
        id='basic-menu'
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        {actions.map((action, key) => (
          <MenuItem key={key} onClick={() => {action.fn(id, type, name); handleClose()}}>
            <ListItemIcon>{action.icon}</ListItemIcon>
            <ListItemText>{action.text}</ListItemText>
          </MenuItem>
        ))}
      </Menu>
    </div>
  )
}

export default ActionList