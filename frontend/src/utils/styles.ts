import { SxProps } from "@mui/material";

export const styles: { [name: string]: SxProps } = {
  mainCard: {
    display: "flex",
    flexDirection: "column",
    px: 2,
    py: 1,
  },

  slimScrollbar: {
    /* width */
    "&::-webkit-scrollbar": {
      width: 6,
    },
    /* Track */
    "&::-webkit-scrollbar-track": {
      background: "#f1f1f1",
    },
    /* Handle */
    "&::-webkit-scrollbar-thumb": {
      background: "#888",
    },
    /* Handle on hover */
    "&::-webkit-scrollbar-thumb:hover": {
      background: "#555",
    },
  } as SxProps,
};
