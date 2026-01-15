import * as React from 'react';
import { cn } from '@/lib/utils';
import { ChevronDown } from 'lucide-react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  children: React.ReactNode;
  className?: string;
}

interface SelectOptionProps extends React.OptionHTMLAttributes<HTMLOptionElement> {
  children: React.ReactNode;
  value: string;
}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(({ className, children, ...props }, ref) => {
  return (
    <div className="relative">
      <select
        ref={ref}
        className={cn(
          'flex h-10 w-full items-center justify-between rounded-lg border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 text-neutral-900 dark:text-white bg-white dark:bg-neutral-800 border-neutral-300 dark:border-neutral-600 appearance-none pr-8',
          className
        )}
        {...props}
      >
        {children}
      </select>
      <ChevronDown className="absolute right-3 top-1/2 h-4 w-4 opacity-50 pointer-events-none -translate-y-1/2" />
    </div>
  );
});

Select.displayName = 'Select';

const SelectOption = ({ children, ...props }: SelectOptionProps) => {
  return <option {...props}>{children}</option>;
};

export {
  Select,
  SelectOption as SelectItem,
  SelectOption,
};