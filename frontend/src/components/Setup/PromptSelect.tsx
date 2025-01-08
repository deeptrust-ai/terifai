import { Select } from "@/components/ui/select";

interface SelectProps {
  selectedSetting: string;
  onSettingChange: (value: string) => void;
}

export const PromptSelect: React.FC<SelectProps> = ({ 
  onSettingChange,
  selectedSetting 
}) => {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-bold">Prompt Customization</h3>
      <Select
        onChange={(e) => {
          console.log('Selected prompt:', e.target.value);
          onSettingChange(e.target.value);
        }}
        defaultValue={selectedSetting}
        icon={null}
      >
        <option value="default" disabled>Select a prompt</option>
        <option value="family">Family Member Distress (Family Impersonation)</option>
        <option value="corporate">Corporate Emergency (C-Suite Impersonation)</option>
        <option value="legal">Law Enforcement/Regulatory Impersonation</option>
      </Select>
    </div>
  );
};