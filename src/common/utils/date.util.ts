export class DateUtil {
  static isExpired(validade: Date): boolean {
    return new Date() > validade;
  }

  static addDays(date: Date, days: number): Date {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  static formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
  }
}





