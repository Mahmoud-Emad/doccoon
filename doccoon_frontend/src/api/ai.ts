import { api } from "@/api/client";

export interface RefineRequest {
  content: string;
  mode: "refine" | "rewrite";
  context?: string;
}

export interface RefineResponse {
  original: string;
  refined: string;
  mode: string;
}

export async function refineContent(
  payload: RefineRequest,
): Promise<RefineResponse | null> {
  const response = await api.post<RefineResponse>("/ai/refine/", payload);
  return response.results ?? null;
}
