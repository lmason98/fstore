import React, { useState } from 'react'
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle, FormControl,
  InputLabel,
  MenuItem,
  Select
} from '@mui/material'


function CopyMoveObjectModal({ copy, curLocation, options, name, open, handleClose, handleSubmit }) {
  const [newLocation, setNewLocation] = useState('')

  const handleChange = (e) => setNewLocation(e.target.value)

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth='sm'>
      <DialogTitle>{copy ? `Copy ${name}` : `Move ${name}`}</DialogTitle>
      <DialogContent>
        <DialogContentText sx={{mb: 2}}>Current location: {curLocation}</DialogContentText>
        <FormControl fullWidth>
          <InputLabel id="copy-move-select-label">New Location</InputLabel>
          <Select
            labelId="copy-move-select-label"
            id="copy-move-select"
            value={newLocation}
            label="New Location"
            onChange={handleChange}
          >
            {options.map((opt, key) => (
              <MenuItem key={key} value={opt.value}>{opt.text}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button variant='contained' onClick={handleClose}>Cancel</Button>
        <Button variant='contained' onClick={() => handleSubmit(newLocation)}>{copy ? 'Copy' : 'Move'}</Button>
      </DialogActions>
    </Dialog>
  )
}

export default CopyMoveObjectModal
