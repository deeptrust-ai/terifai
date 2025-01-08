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
    <Select
      onChange={(e) => onSettingChange(e.target.value)}
      defaultValue={selectedSetting}
      icon={null}
    >
      <option value="default" disabled>Select a prompt</option>
      <option value="casual">Casual Conversation</option>
      <option value="professional">Professional Meeting</option>
      <option value="interview">Interview Mode</option>
      <option value="creative">Creative Discussion</option>
    </Select>
  );
};