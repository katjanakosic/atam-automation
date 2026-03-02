"use client"

import React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

const STEPS = [
  { href: "/introduction", label: "Introduction" },
  { href: "/input", label: "Input" },
  { href: "/output", label: "Output" },
] as const

const DETAIL_PAGES: Record<string, string> = {
  "/output/sensitivities": "Component Sensitivities",
  "/output/tradeoffs": "Tradeoffs",
}

export function StepNav() {
  const pathname = usePathname()

  const currentStepIndex = STEPS.findIndex(
    (s) => pathname === s.href || pathname.startsWith(s.href + "/")
  )

  const detailLabel = DETAIL_PAGES[pathname]

  return (
    <Breadcrumb>
      <BreadcrumbList>
        {STEPS.map((step, i) => {
          const isActive = i === currentStepIndex && !detailLabel
          const isPast = i < currentStepIndex
          const isParentOfDetail = i === currentStepIndex && !!detailLabel

          return (
            <React.Fragment key={step.href}>
              {i > 0 && <BreadcrumbSeparator />}
              <BreadcrumbItem>
                {isActive ? (
                  <BreadcrumbPage>{step.label}</BreadcrumbPage>
                ) : isPast || isParentOfDetail ? (
                  <BreadcrumbLink asChild>
                    <Link href={step.href}>{step.label}</Link>
                  </BreadcrumbLink>
                ) : (
                  <span className="text-muted-foreground">{step.label}</span>
                )}
              </BreadcrumbItem>
            </React.Fragment>
          )
        })}

        {detailLabel && (
          <>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage>{detailLabel}</BreadcrumbPage>
            </BreadcrumbItem>
          </>
        )}
      </BreadcrumbList>
    </Breadcrumb>
  )
}
