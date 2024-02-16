import {useState} from "react";
import api from "../../utils/api";


function Upload() {

  const [file, setFile] = useState()

  const handleFileChange = (e) => {
    if (e.target.files)
      setFile(e.target.files[0])
  }

  const handleUploadClick = () => {
    if (!file) {
      return;
    }

    let formData = new FormData()
    formData.append('files', file)

    api.post('/upload/', formData)
      .then(resp => {
        console.log('api post resp :', resp)
      })
      .catch(err => {
        console.log('api post err :', err)
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