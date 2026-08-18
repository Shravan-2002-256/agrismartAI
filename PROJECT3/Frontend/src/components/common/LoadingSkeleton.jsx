import React from 'react';

export const CardSkeleton = () => (
  <div className="card-pro animate-pulse">
    <div className="flex items-start justify-between mb-4">
      <div className="space-y-3 flex-1">
        <div className="skeleton-title"></div>
        <div className="skeleton-text w-4/5"></div>
      </div>
      <div className="skeleton-circle w-12 h-12"></div>
    </div>
    <div className="space-y-2">
      <div className="skeleton-text"></div>
      <div className="skeleton-text w-3/4"></div>
    </div>
  </div>
);

export const StatCardSkeleton = () => (
  <div className="stat-card animate-pulse">
    <div className="space-y-2 flex-1">
      <div className="skeleton h-4 w-24"></div>
      <div className="skeleton h-8 w-16"></div>
      <div className="skeleton h-3 w-32"></div>
    </div>
    <div className="skeleton-circle w-12 h-12"></div>
  </div>
);

export const TableRowSkeleton = () => (
  <tr className="animate-pulse">
    <td className="px-4 py-3">
      <div className="skeleton h-4 w-32"></div>
    </td>
    <td className="px-4 py-3">
      <div className="skeleton h-4 w-24"></div>
    </td>
    <td className="px-4 py-3">
      <div className="skeleton h-4 w-20"></div>
    </td>
    <td className="px-4 py-3">
      <div className="skeleton h-6 w-16 rounded-full"></div>
    </td>
  </tr>
);

export const ListItemSkeleton = () => (
  <div className="flex items-center space-x-4 p-4 border-b border-gray-200 dark:border-gray-700 animate-pulse">
    <div className="skeleton-circle w-12 h-12 flex-shrink-0"></div>
    <div className="flex-1 space-y-2">
      <div className="skeleton h-4 w-3/4"></div>
      <div className="skeleton h-3 w-1/2"></div>
    </div>
  </div>
);

export const DashboardSkeleton = () => (
  <div className="space-y-6">
    <div className="skeleton-title w-48 mb-6"></div>
    
    {/* Stats Grid */}
    <div className="grid md:grid-cols-3 gap-6">
      <StatCardSkeleton />
      <StatCardSkeleton />
      <StatCardSkeleton />
    </div>
    
    {/* Content Cards */}
    <div className="grid md:grid-cols-2 gap-6">
      <CardSkeleton />
      <CardSkeleton />
    </div>
  </div>
);

export const PageSkeleton = () => (
  <div className="space-y-6 animate-pulse">
    <div className="skeleton-title w-64"></div>
    <div className="skeleton-text w-96"></div>
    <div className="grid gap-6 mt-8">
      <CardSkeleton />
      <CardSkeleton />
    </div>
  </div>
);

export default CardSkeleton;
