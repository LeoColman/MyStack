import { Distribution, Progress } from '~/domain/models/metrics/metrics'

export interface MetricsRepository {
  fetchCategoryDistribution(projectId: string): Promise<Distribution>
  fetchSpanDistribution(projectId: string): Promise<Distribution>
  fetchMemberProgress(projectId: string): Promise<Progress>
}
