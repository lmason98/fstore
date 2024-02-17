import React, { useState } from 'react'
import { Box, Button, Grid, Typography } from '@mui/material'
import { CreateNewFolder, FileUpload, Refresh } from '@mui/icons-material'

import Upload from '../upload/upload'
import NewFolderModal from '../newFolderModal/newFolderModal'
import FileBrowser from '../fileBrowser/fileBrowser'
import api from '../../utils/api'
import { useAlert } from '../alert/alert'
import UploadFileModal from "../uploadFileModal/uploadFileModal";


function Content() {
  const doAlert = useAlert()

  const [location, setLocation] = useState('/')
  const [newFolderModalOpen, setNewFolderModalOpen] = useState(false)
  const [uploadFileModalOpen, setUploadFileModalOpen] = useState(false)
  const [refreshFileBrowser, setRefreshFileBrowser] = useState(false)

  const doRefreshFileBrowser = () => setRefreshFileBrowser(!refreshFileBrowser)

  const openNewFolderModal = () => setNewFolderModalOpen(true)
  const closeNewFolderModal = () => setNewFolderModalOpen(false)
  const submitNewFolder = folderName => {

    api.post('/folder/', {name: folderName, location: location})
      .then(resp => {
        doAlert(resp.data.message, resp.data.status)
        if (resp.data.status === 'success')
          doRefreshFileBrowser()
      })

    closeNewFolderModal()
  }

  const openUploadFileModal = () => setUploadFileModalOpen(true)
  const closeUploadFileModal = () => setUploadFileModalOpen(false)
  const submitUploadFile = (formData, fileName) => {

    formData.append('location', location)

    api.post('/file/', formData)
      .then(resp => {
        doAlert(resp.data.message, resp.data.status)

        if (resp.data.status === 'success') {
          closeUploadFileModal()
          doRefreshFileBrowser()
        }
      })
  }

  const enterFolder = (newLocation, forward) => {
    if (forward)
      setLocation(location + newLocation)
    else
      setLocation(newLocation)
  }

  return (
    <>
      <Box sx={{display: 'flex', width: '100%'}}>
        <Grid
          container
          spacing={0}
          direction='column'
          sx={{height: '100vh', backgroundColor: '#eaeaea', p: 5}}
        >
          {/* Actions */}
          <Grid item container spacing={5}>
            <Grid item>
              <Button startIcon={<CreateNewFolder />} variant='contained' size='large' onClick={openNewFolderModal}>
                Create Folder
              </Button>
            </Grid>
            <Grid item>
              <Button startIcon={<FileUpload />} variant='contained' size='large' onClick={openUploadFileModal}>
                Upload File
              </Button>
            </Grid>
            <Grid item>
              <Button startIcon={<Refresh />} variant='contained' size='large' onClick={doRefreshFileBrowser}>
                Refresh
              </Button>
            </Grid>
          </Grid>

          {/* File browser */}
          <Grid item mt={5}><Typography variant='h4'>My Files: {location}</Typography></Grid>
          <Grid item mt={5}>
            <FileBrowser location={location} refresh={refreshFileBrowser} enterFolder={enterFolder} />
          </Grid>
        </Grid>
      </Box>

      <NewFolderModal open={newFolderModalOpen} location={location} handleClose={closeNewFolderModal}
                      onSubmit={submitNewFolder} />
      <UploadFileModal open={uploadFileModalOpen} location={location} handleClose={closeUploadFileModal}
                       onSubmit={submitUploadFile} />
    </>
  )
}

export default Content