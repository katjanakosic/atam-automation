import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"

interface PageNavigationProps {
  previousHref?: string
  previousLabel?: string
  nextHref?: string
  nextLabel?: string
}

export function PageNavigation({
  previousHref,
  previousLabel = "Previous",
  nextHref,
  nextLabel = "Next",
}: PageNavigationProps) {
  return (
    <div className="flex justify-between items-center pt-8">
      {previousHref ? (
        <Button variant="outline" asChild>
          <Link href={previousHref}>
            <ChevronLeft className="mr-2 h-4 w-4" />
            {previousLabel}
          </Link>
        </Button>
      ) : (
        <div />
      )}
      {nextHref ? (
        <Button asChild>
          <Link href={nextHref}>
            {nextLabel}
            <ChevronRight className="ml-2 h-4 w-4" />
          </Link>
        </Button>
      ) : (
        <div />
      )}
    </div>
  )
}
