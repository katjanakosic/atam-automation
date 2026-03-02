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
  const color = getSensitivityColor(value)

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className={cn("flex items-center gap-2", className)}>
            <div className="h-2 w-24 rounded-full bg-muted overflow-hidden">
              <div
                className="h-full rounded-full transition-all"
                style={{ width: `${percentage}%`, backgroundColor: color }}
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
