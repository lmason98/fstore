import React, { useState } from 'react'
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material'

import { useAlert } from '../alert/alert'


function UploadFileModal({ open, location, handleClose, onSubmit }) {
  const doAlert = useAlert()

  const [file, setFile] = useState()

  const handleFileChange = (e) => {
    if (e.target.files)
      setFile(e.target.files[0])
  }

  const handleUploadClick = () => {
    if (!file) {
      doAlert('No file selected!', 'error')
      return
    }

    let formData = new FormData()
    formData.append('files', file)

    onSubmit(formData, file.name)
  }

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth='sm'>
      <DialogTitle>Upload file</DialogTitle>
      <DialogContent>
        <DialogContentText>Parent: {location}</DialogContentText>

        <input type='file' onChange={handleFileChange} />

        <div>{file && `${file.name} - ${file.type}`}</div>

      </DialogContent>
      <DialogActions>
        <Button variant='contained' onClick={handleClose}>Cancel</Button>
        <Button variant='contained' onClick={handleUploadClick}>Upload</Button>
      </DialogActions>
    </Dialog>
  )
}

export default UploadFileModal