import { useState } from "react";
import api from "../../utils/api";
import {useAlert} from "../alert/alert";


function Upload() {
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

    api.post('/upload/', formData)
      .then(resp => {
        if (resp.data.status === 'success')
          doAlert(`Successfully uploaded ${file.name}`, 'success')
        else
          doAlert(resp.data.message, resp.data.status)
      })
      .catch(err => {
        console.log('err :', err)
        // doAlert(resp.data.message, resp.data.status)
      })

  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />

      <div>{file && `${file.name} - ${file.type}`}</div>

      <button onClick={handleUploadClick}>Upload</button>
    </div>
  );}

export default Upload