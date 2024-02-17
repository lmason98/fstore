import React, { useState } from 'react'
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@mui/material'

function NewFolderModal({ open, location, handleClose, onSubmit }) {
  const [folderName, setFolderName] = useState('')

  const handleSubmit = () => {
    onSubmit(folderName)
    setFolderName('')
  }

  const handleName = (e) => setFolderName(e.target.value)

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth='sm'>
      <DialogTitle>Create New Folder</DialogTitle>
      <DialogContent>
        <DialogContentText>Parent: {location}</DialogContentText>
        <DialogContentText>Enter New Folder Name</DialogContentText>
        <TextField
          sx={{width: '100%', mt: 1}} label='Folder Name' value={folderName} onChange={handleName}
        />
      </DialogContent>
      <DialogActions>
        <Button variant='contained' onClick={handleClose}>Cancel</Button>
        <Button variant='contained' onClick={handleSubmit}>Create</Button>
      </DialogActions>
    </Dialog>
  )
}

export default NewFolderModal