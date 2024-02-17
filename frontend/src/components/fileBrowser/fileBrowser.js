import {
  Box, Button,
  CircularProgress, Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material'
import { Folder, InsertDriveFile, ArrowBack, Delete } from '@mui/icons-material'

import './fileBrowser.css'
import React, { useEffect, useState } from 'react'
import api from "../../utils/api";
import ActionList from "../actionList/actionList";
import {useAlert} from "../alert/alert";

function FileBrowser({ location, refresh, enterFolder }) {
  const doAlert = useAlert()

  const [loading, setLoading] = useState(true)
  const [data, setData] = useState([])

  const getData = () => {
    setLoading(true)

    api.get(`/folder?location=${location}`)
      .then(resp => {
        setData(resp.data.objects)
        setLoading(false)
      })
  }

  useEffect(() => {
    getData()
  }, [location, refresh])

  // move down one folder
  const handleFolderClick = (object) => {
    if (object.type === 'folder')
      enterFolder(object.name + '/', true)
  }

  // move up one folder
  const enterParentFolder = () => {
    // trim off last '<location>/'
    const secondLastIndex = location.lastIndexOf('/', location.lastIndexOf('/') - 1)
    const newLocation = location.substring(0, secondLastIndex + 1)

    enterFolder(newLocation, false)
  }

  // actions
  const deleteObject = (id, type, name) => {

    let message;
    if (type === 'folder') {
      message = 'Deleting a folder will delete all of its sub-content.'
    } else
      message = `Delete ${name}?`

    if (window.confirm(message))
      api.delete(`/${type}/${id}/`)
        .then(resp => {
          doAlert(resp.data.message, resp.data.status)

          if (resp.data.status === 'success')
            setData([...data.filter(obj => `${obj.id}${obj.type}` !== `${id}${type}`)])
        })
  }

  const generateActions = () => {
    let actions = [
      {fn: deleteObject, text: 'Delete', icon: <Delete />},
    ]

    return actions
  }

  return (
    loading ?
      <Box sx={{display: 'flex', textAlign: 'center', height: '100%'}}>
        <CircularProgress sx={{margin: 'auto auto'}} />
      </Box>
    :
      <>
        {location !== '/' ?
          <Button startIcon={<ArrowBack />} variant='contained' sx={{mb: 2}} onClick={enterParentFolder}>Back</Button>
          : <></>}
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{width: '5%'}}> </TableCell>
                <TableCell sx={{width: '65%'}}>Name</TableCell>
                <TableCell sx={{width: '10%'}}>Size</TableCell>
                <TableCell sx={{width: '10%'}}>Updated</TableCell>
                <TableCell align='right' sx={{width: '10%'}}> </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.length === 0 ?
                <TableRow>
                  <TableCell align='center' colSpan='5' sx={{fontWeight: 'bold'}}>No data</TableCell>
                </TableRow>
                :
                data.map((object, key) => (
                  <TableRow key={key} className={`body ${object.type}`}>
                    <TableCell onClick={() => handleFolderClick(object)}>
                      {object.type === 'folder' ? <Folder /> : <InsertDriveFile />}
                    </TableCell>
                    <TableCell onClick={() => handleFolderClick(object)}>
                      {object.name}
                    </TableCell>
                    <TableCell onClick={() => handleFolderClick(object)}>
                      {object.type === 'file' ? object.size : '-'}
                    </TableCell>
                    <TableCell onClick={() => handleFolderClick(object)}>
                      {object.updated}
                    </TableCell>
                    <TableCell align='right'>
                      <ActionList objectInfo={{id: object.id, type: object.type, name: object.name}}
                                  actions={generateActions()} />
                    </TableCell>
                  </TableRow>
                ))
              }
            </TableBody>
          </Table>
        </TableContainer>
      </>
  )
}

export default FileBrowser