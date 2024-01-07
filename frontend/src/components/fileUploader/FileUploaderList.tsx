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
        px: 3,
        py: 1.5,
        columnGap: 2,
      }}
    >
      {files.length ? (
        files.map((fileData, i) => (
          <Box
            key={i}
            sx={(theme) => ({
              width: {
                xs: "100%",
                sm: "calc(50% - 8px)",
                md: "100%",
                lg: "calc(50% - 8px)",
              },
              "&:hover": {
                bgcolor: `${theme.palette.primary.main}30`,
              },
              borderTopLeftRadius: 10,
              borderTopRightRadius: 10,
              borderRadius: 2,
            })}
          >
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                px: 1,
                py: 0.5,
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
          }}
        >
          No files selected
        </Box>
      )}
    </Box>
  );
};

export default FileUploaderList;
