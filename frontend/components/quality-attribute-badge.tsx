import { Badge } from "@/components/ui/badge"
import { getQAColor } from "@/lib/constants"
import { cn } from "@/lib/utils"

interface QualityAttributeBadgeProps {
  attribute: string
  className?: string
}

export function QualityAttributeBadge({
  attribute,
  className,
}: QualityAttributeBadgeProps) {
  const color = getQAColor(attribute)
  return (
    <Badge
      variant="outline"
      className={cn(color.bg, color.text, color.border, className)}
    >
      {attribute}
    </Badge>
  )
}
