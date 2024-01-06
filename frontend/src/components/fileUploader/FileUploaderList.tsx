import { Dispatch, SetStateAction } from "react";
import { Box, Divider, IconButton, Typography } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";

import { styles } from "../../utils/styles";

interface Props {
  files: FileData[];
  setFiles: Dispatch<SetStateAction<FileData[]>>;
}

const FileUploaderList = ({ files, setFiles }: Props) => {
  return (
    <Box
      sx={{
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
        px: 2,
        py: 1,
        gap: 1,
        color: "text.primary"
      }}
    >
      {files.length ? (
        files.map((fileData, i) => (
          <Box
            key={i}
            sx={{
              width: {
                xs: "100%",
                sm: "calc(50% - 4px)",
                md: "100%",
                lg: "calc(50% - 4px)",
              },
            }}
          >
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                px: 1,
              }}
            >
              <Typography
                sx={{
                  width: "100%",
                  fontSize: 14,
                }}
                noWrap
              >
                {fileData.name}
              </Typography>

              <IconButton
                sx={{
                  p: 0.25,
                }}
                onClick={() => setFiles(files.filter((_, fi) => fi !== i))}
              >
                <DeleteIcon />
              </IconButton>
            </Box>

            <Divider />
          </Box>
        ))
      ) : (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            width: "100%",
            height: "100%",
          }}
        >
          No files selected
        </Box>
      )}
    </Box>
  );
};

export default FileUploaderList;
