declare interface Step {
  id: number;
  status: "loading" | "success" | "failed";
  specialDescription?: string;
}
