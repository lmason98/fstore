import React, { createContext, useContext, useState } from 'react'
import { Snackbar, Alert } from '@mui/material'

const AlertContext = createContext();

export const useAlert = () => {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error('useAlert must be used within an AlertProvider');
  }
  return context;
};

function AlertProvider({ children }) {
  const [open, setOpen] = useState(false)
  const [message, setMessage] = useState('')
  const [severity, setSeverity] = useState('info')
  
  const showAlert = (newMessage, newSeverity = 'info') => {
    setMessage(newMessage)
    setSeverity(newSeverity)
    setOpen(true)
  }
  
  const hideAlert = () => {
    setOpen(false)
  }
  
  return (
    <AlertContext.Provider value={showAlert}>
      {children}
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={hideAlert}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity={severity}>
          {message}
        </Alert>
      </Snackbar>
    </AlertContext.Provider>
  )
}

export default AlertProvider