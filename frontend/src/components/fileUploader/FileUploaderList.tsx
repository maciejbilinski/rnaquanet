import { Dispatch, SetStateAction } from "react";
import {
  Box,
  Divider,
  IconButton,
  MenuItem,
  TextField,
  Typography,
} from "@mui/material";
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
        "&::-webkit-scrollbar-track": {
          borderTopRightRadius: 3,
          borderBottomRightRadius: 3,
        },
        " &::-webkit-scrollbar-thumb": {
          borderRadius: 10,
        },
        border: "1px solid",
        borderColor: "gray",
        borderRadius: 1,
        color: "text.primary",
        display: "flex",
        flexBasis: "50%",
        alignContent: "flex-start",
        flexWrap: "wrap",
        height: "100%",
        overflowY: "auto",
        p: 1,
        columnGap: 2,
      }}
    >
      {files.length ? (
        files.map((fileData, i) => (
          <Box
            key={i}
            sx={(theme) => ({
              // width: {
              //   xs: "100%",
              //   sm: "calc(50% - 8px)",
              //   md: "100%",
              //   lg: "calc(50% - 8px)",
              // },
              width: "100%",
              "&:hover": {
                bgcolor: `${theme.palette.primary.main}30`,
              },
              borderRadius: 2,
            })}
          >
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                p: 1,
                gap: 0.5,
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

              <TextField
                label="Model"
                size="small"
                sx={{ minWidth: 70 }}
                value={fileData.selectedModel ?? null}
                onChange={(event) =>
                  setFiles((old) =>
                    old.map((file) =>
                      file.name == fileData.name
                        ? {
                            ...file,
                            selectedModel: event.target.value,
                          }
                        : file
                    )
                  )
                }
                select
              >
                {Object.keys(fileData.models!).map((model, i) => (
                  <MenuItem key={i} value={model}>
                    {model}
                  </MenuItem>
                ))}
              </TextField>

              <TextField
                label="Chain"
                size="small"
                sx={{ minWidth: 70 }}
                value={fileData.selectedChain ?? null}
                onChange={(event) =>
                  setFiles((old) =>
                    old.map((file) =>
                      file.name == fileData.name
                        ? {
                            ...file,
                            selectedChain: event.target.value,
                          }
                        : file
                    )
                  )
                }
                select
              >
                {fileData.models![fileData.selectedModel!].map((chain, i) => (
                  <MenuItem key={i} value={chain}>
                    {chain}
                  </MenuItem>
                ))}
              </TextField>

              <IconButton
                sx={{
                  color: "text.secondary",
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
            fontSize: 14,
          }}
        >
          No files selected
        </Box>
      )}
    </Box>
  );
};

export default FileUploaderList;
