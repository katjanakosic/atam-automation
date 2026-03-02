import { getSensitivityColor } from "@/lib/constants"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"

interface SensitivityBarProps {
  value: number
  className?: string
}

export function SensitivityBar({ value, className }: SensitivityBarProps) {
  const percentage = Math.round(value * 100)
  const colorClass = getSensitivityColor(value)

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className={cn("flex items-center gap-2", className)}>
            <div className="h-2 w-24 rounded-full bg-muted overflow-hidden">
              <div
                className={cn("h-full rounded-full transition-all", colorClass)}
                style={{ width: `${percentage}%` }}
              />
            </div>
            <span className="text-sm font-medium tabular-nums">
              {value.toFixed(2)}
            </span>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p>
            Sensitivity: {value.toFixed(3)} ({percentage}%)
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
