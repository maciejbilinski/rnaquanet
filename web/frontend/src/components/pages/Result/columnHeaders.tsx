import { GridColDef } from "@mui/x-data-grid";
import { type MRT_ColumnDef } from "material-react-table";

export const columnHeaders: MRT_ColumnDef<FileResult>[] = [
  {
    accessorKey: "name",
    header: "File name",
  },
  {
    header: "Model",
    accessorFn: (row) => Number(row.selectedModel) + 1,
  },
  { accessorKey: "selectedChain", header: "Chain" },
  {
    accessorKey: "rmsd",
    header: "Average RMSD",
    accessorFn: (row) =>
      row.status === "SUCCESS" && row.rmsd
        ? row.rmsd.toFixed(4)
        : "Invalid file!",
    muiTableHeadCellProps: {
      align: "right",
    },
    muiTableBodyCellProps: {
      align: "right",
    },
    muiTableFooterCellProps: {
      align: "right",
    },
  },
];

export const columnHeadersDesc: GridColDef<Descriptor>[] = [
  {
    field: "name",
    headerName: "Descriptor name",
    flex: 1,
  },
  {
    field: "residue_range",
    headerName: "Residue range",
    flex: 1,
  },
  {
    field: "sequence",
    headerName: "Sequence",
    flex: 1,
  },
  {
    field: "rmsd",
    headerName: "RMSD",
    valueFormatter: (row) => row.value.toFixed(4),
    type: "number",
    flex: 1,
  },
];