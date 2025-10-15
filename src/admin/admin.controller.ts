import { Controller, Post, Get, Body, HttpCode, HttpStatus, Param, UseGuards } from '@nestjs/common';
import { AdminService, LoginAdminDto, CreateMaeDto, CreateFilhoDto } from './admin.service';
import { MasterAdminGuard } from './guards/master-admin.guard';

@Controller()
export class AdminController {
  constructor(private readonly adminService: AdminService) {}

  @Post('admin/login-master')
  @HttpCode(HttpStatus.OK)
  async loginMasterAdmin(@Body() loginAdminDto: LoginAdminDto) {
    return this.adminService.loginMasterAdmin(loginAdminDto);
  }

  @Post('admin/create-mae')
  @UseGuards(MasterAdminGuard)
  async createMae(@Body() createMaeDto: CreateMaeDto) {
    return this.adminService.createMae(createMaeDto);
  }

  @Post('admin/create-filho')
  @UseGuards(MasterAdminGuard)
  async createFilho(@Body() createFilhoDto: CreateFilhoDto) {
    return this.adminService.createFilho(createFilhoDto);
  }

  @Get('admin/maes')
  @UseGuards(MasterAdminGuard)
  async getAllMaes() {
    return this.adminService.getAllMaes();
  }

  @Get('admin/filhos')
  @UseGuards(MasterAdminGuard)
  async getAllFilhos() {
    return this.adminService.getAllFilhos();
  }

  @Get('api/names/:userId/:userType')
  async getNames(
    @Param('userId') userId: string,
    @Param('userType') userType: string,
  ) {
    return this.adminService.getNames(userId, userType);
  }


}