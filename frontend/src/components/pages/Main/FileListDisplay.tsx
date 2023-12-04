import { Dispatch, SetStateAction } from "react";
import { Box, IconButton, Typography } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

import { styles } from "../../../utils/styles";

interface FileListProps {
  files: File[];
  setFiles: Dispatch<SetStateAction<File[]>>;
}

const FileListDisplay = ({ files, setFiles }: FileListProps) => {
  return (
    <Box sx={{
      ...styles.slimScrollbar,
      display: "flex",
      alignContent: "flex-start",
      flexWrap: "wrap",
      width: "100%",
      height: "100%",
      overflowY: "auto",
      border: "1px solid",
      borderColor: "gray",
      borderRadius: 1,
      pl: 2,
      pr: 1,
      py: 1,
    }}>
      {files.length ? (
        files.map((file, i) => (
          <Box key={i} sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            width: "50%",
            px: 1,
          }}>
            <Typography sx={{
              fontSize: 14,
            }} noWrap>
              {file.name}
            </Typography>

            <IconButton
              sx={{
                p: 0.25,
              }}
              onClick={() => setFiles(
                files.filter((_, fi) => fi !== i)
              )}
            >
              <DeleteIcon />
            </IconButton>
          </Box>
        ))
      ) : (
        <Box sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          height: "100%",
        }}>
          <Typography>No files selected.</Typography>
        </Box>
      )}
    </Box>
  );
};

export default FileListDisplay;